import importlib.util,sys,runpy
spec=importlib.util.spec_from_file_location("src.moment_component_audit","/workspace/mitosis-day15-stage/src/moment_component_audit.py")
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
sys.argv=["day15_moment_integrity", "--device", "cpu"]
runpy.run_path("/workspace/mitosis-day15-stage/experiments/day15_moment_integrity.py",run_name="__main__")
