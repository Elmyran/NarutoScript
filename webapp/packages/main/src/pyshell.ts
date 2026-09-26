import {alasPath, pythonPath} from '/@/config';
import logger from '/@/logger';

const {PythonShell} = require('python-shell');
const {spawn} = require('child_process');
const treeKill = require('tree-kill');

/** All live shells — must be reaped before Electron exits. */
const liveShells = new Set<PyShell>();

function killPidTree(pid: number | undefined): Promise<void> {
  return new Promise(resolve => {
    if (!pid) {
      resolve();
      return;
    }
    // taskkill /T is more reliable than SIGTERM for python.exe → uvicorn children
    if (process.platform === 'win32') {
      const killer = spawn('taskkill', ['/PID', String(pid), '/T', '/F'], {
        stdio: 'ignore',
        windowsHide: true,
      });
      killer.on('close', () => resolve());
      killer.on('error', () => {
        treeKill(pid, 'SIGKILL', () => resolve());
      });
      return;
    }
    treeKill(pid, 'SIGKILL', () => resolve());
  });
}

export class PyShell extends PythonShell {
  /** Set when we terminate this shell on purpose (window close / quit). */
  killing = false;

  constructor(script: string, args: Array<string> = []) {
    const options = {
      mode: 'text',
      args: args,
      pythonPath: pythonPath,
      scriptPath: alasPath,
    };
    logger.info(`${pythonPath} ${script} ${args}`);
    super(script, options);
    liveShells.add(this);
    // Drop finished shells so a later quit can never taskkill a reused pid.
    super.on('close', () => {
      liveShells.delete(this);
    });
  }

  on(event: string, listener: (...args: any[]) => void): this {
    this.removeAllListeners(event);
    super.on(event, listener);
    return this;
  }

  /**
   * Wrap python-shell's end callback.
   *
   * python-shell reports *any* non-zero exit code through this callback with the
   * accumulated stderr as the error message. Our own `taskkill /T /F` therefore
   * looks like a crash, and callers that rethrow (serviceLogic/createAlas.ts does
   * `throw err`) turned that into an uncaught main-process exception — Electron
   * then showed the "A JavaScript error occurred in the main process" dialog on
   * every exit. Neither an intentional kill nor a caller's throw may escape here.
   */
  end(callback?: (...args: any[]) => any): this {
    return super.end((err: any, exitCode: number, exitSignal: string) => {
      if (this.killing) {
        logger.info(`PyShell killed on purpose, ignoring exit code ${exitCode}`);
        return;
      }
      try {
        return callback ? callback(err, exitCode, exitSignal) : undefined;
      } catch (e) {
        logger.error('PyShell.end callback threw (ignored):' + e);
        return undefined;
      }
    });
  }

  kill(callback: (...args: any[]) => void): this {
    this.killAsync().finally(() => {
      try {
        callback();
      } catch (e) {
        logger.error('PyShell.kill callback:' + e);
      }
    });
    return this;
  }

  async killAsync(): Promise<void> {
    this.killing = true;
    liveShells.delete(this);
    const child = this.childProcess;
    // Process already gone (or never spawned): do not taskkill a pid the OS may
    // have reused for something else.
    if (!child || child.exitCode !== null || child.signalCode !== null) {
      return;
    }
    const pid = child.pid;
    try {
      await killPidTree(pid);
    } catch (e) {
      logger.error('PyShell.killAsync:' + e);
    }
  }
}

/** Kill every spawned python service and wait until the trees are gone. */
export async function killAllPyShells(): Promise<void> {
  const pending = [...liveShells].map(s => s.killAsync());
  liveShells.clear();
  await Promise.all(pending);
}
