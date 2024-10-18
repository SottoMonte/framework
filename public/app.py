# Import
import sys
import os

if sys.platform == 'emscripten':
    run = load_module(area="framework",service='service',adapter='run')
else:
    cwd = os.getcwd()
    sys.path.insert(1, cwd+'/src')
    import framework.service.language as language

    run = language.load_module(area="framework",service='service',adapter='run')


if __name__ == "__main__":
    run.application(args=sys.argv)
    