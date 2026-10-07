import importlib.util,sys,runpy
for name,file in [("src.moment_component_audit","src/moment_component_audit.py"),("experiments.day15_moment_report","experiments/day15_moment_report.py")]:
 spec=importlib.util.spec_from_file_location(name,"/workspace/mitosis-day15-stage/"+file)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
for file in ["day15_report_integrity.py","day16_bert_integrity.py"]:
 sys.argv=[file,"--device","cpu"] if "bert" in file else [file]
 runpy.run_path("/workspace/mitosis-day15-stage/experiments/"+file,run_name="__main__")
