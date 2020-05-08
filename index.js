const core = require("@actions/core");
const glob = require("@actions/glob");
const exec = require("@actions/exec");

async function run() {
  // const buildPath = core.getInput("path");

  // const options = {};
  // options.listeners = {
  //   stdout: (data) => {
  //     myOutput += data.toString();
  //   },
  //   stderr: (data) => {
  //     myError += data.toString();
  //   },
  // };

  try {
    await exec.exec("ls -la");
    await exec.exec("python cldr-coverage.py");
  } catch (error) {
    core.setFailed(
      `cldr-coverage Action failed during execution with error: ${error.message}`
    );
  }
}

run();
