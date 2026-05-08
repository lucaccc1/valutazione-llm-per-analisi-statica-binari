import idautils
import idaapi
import ida_auto
import idc
import json
import os
import sys

if not idaapi.init_hexrays_plugin():
    print("ida is not available.")
    sys.exit(1)

ground_truth = {}
print("start extracting ground truth.")

ida_auto.auto_wait()
idc.plan_and_wait(idc.get_inf_attr(idc.INF_MIN_EA), idc.get_inf_attr(idc.INF_MAX_EA))

for func in idautils.Functions():
    func_name = idc.get_func_name(func)
    flags = idc.get_func_attr(func, idc.FUNCATTR_FLAGS)

    nomi_spazzatura = ["frame_dummy", "deregister_tm_clones", "register_tm_clones", "printf", "_init", "_fini", "start"]

    if (flags & idaapi.FUNC_LIB) or (flags & idaapi.FUNC_THUNK) or func_name.startswith(("_", ".")) or func_name in nomi_spazzatura:
        continue

    if func_name.startswith("sub_"):
        continue

    variabili_funzione = {}
    try:
        cfunc = idaapi.decompile(func)
        if cfunc:
            for lvar in cfunc.get_lvars():
                if lvar.name and lvar.name != "retaddr":
                    variabili_funzione[lvar.name] = ""
    except Exception as e:
        pass 

    ground_truth[hex(func)] = {
        "nome_funzione_originale": func_name,
        "variabili": variabili_funzione 
    }

percorso_binario = idc.get_input_file_path() 

if 'bin_debug/' in percorso_binario:
    rel_path = percorso_binario.split('bin_debug/')[-1]
else:
    rel_path = os.path.basename(percorso_binario)

sub_dir = os.path.dirname(rel_path)
nome_base = os.path.splitext(os.path.basename(percorso_binario))[0]

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_dir = os.path.join(base_dir, 'data', 'ground_truth', sub_dir)
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, f"{nome_base}.json")

with open(output_path, 'w') as f:
    json.dump(ground_truth, f, indent=4)

print(f"extraction completed. data saved to: {output_path}")

if idaapi.cvar.batch:
    idc.qexit(0)