import Options, Utils
from os import unlink, symlink, popen
from os.path import exists 

srcdir = '.'
blddir = 'build'
VERSION = '0.0.9'

def set_options(opt):
  opt.tool_options('compiler_cxx')

def configure(conf):
  conf.check_tool('compiler_cxx')
  conf.check_tool('node_addon')

  fb_config = conf.find_program('fb_config', var='FB_CONFIG')
  if not fb_config:
    fb_libdir = "-L/usr/lib -lfbclient"
    fb_includedir = "-I/usr/include/"
  else:    
    fb_libdir = popen("%s --libs" % fb_config).readline().strip()
    fb_includedir = popen("%s --cflags" % fb_config).readline().strip()
  conf.env.append_value("LIBPATH_FB", fb_libdir)
  conf.env.append_value("LIB_FB", "fbclient")
  conf.env.append_value("CPPPATH_FB", fb_includedir)

def buildo(bldo):
  obj = bldo.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'binding'
  obj.source = "./src/binding.cc"
  obj.uselib = "FB"
  
def build(bld):
  obj = bld.new_task_gen('cxx', 'shlib', 'node_addon')
  obj.target = 'binding'
  obj.source = "./src/fb-bindings.cc ./src/fb-bindings-connection.cc ./src/fb-bindings-eventblock.cc ./src/fb-bindings-fbeventemitter.cc ./src/fb-bindings-fbresult.cc ./src/fb-bindings-blob.cc ./src/fb-bindings-statement.cc"
  obj.uselib = "FB"

def test(tst):
  node_binary = 'node'
  
  if not exists('./tools/nodeunit/bin/nodeunit'):
    print("\033[31mNodeunit doesn't exists.\033[39m\nYou should run `git submodule update --init` before run tests.")
    exit(1)
  else:
    Utils.exec_command(node_binary + ' ./tools/nodeunit/bin/nodeunit tests/def')

def test_current(tstc):
  node_binary = 'node'
  
  if not exists('./tools/nodeunit/bin/nodeunit'):
    print("\033[31mNodeunit doesn't exists.\033[39m\nYou should run `git submodule update --init` before run tests.")
    exit(1)
  else:
    Utils.exec_command(node_binary + ' ./tools/nodeunit/bin/nodeunit tests/current')
