

-- Local Variables
local name = "geopandas"
local version= "0.2.1"

-- Locate Home Directory
local homedir = os.getenv("INSTALLS")
local root = pathJoin(homedir, "local", name, version)

-- Set Basic Paths
prepend_path("PYTHONPATH", pathJoin(root, "lib/python2.7/site-packages"))
prepend_path(root, "bin")

