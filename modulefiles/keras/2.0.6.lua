

-- Local Variables
local name = "keras"
local version= "2.0.6"

-- Locate Home Directory
local homedir = os.getenv("INSTALLS")
local root = pathJoin(homedir, "local", name, version)

-- Set Basic Paths
prepend_path("PYTHONPATH", pathJoin(root, "lib/python2.7/site-packages"))
prepend_path(root, "bin")

