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

ida_auto.auto_wait()
idc.plan_and_wait(idc.get_inf_attr(idc.INF_MIN_EA), idc.get_inf_attr(idc.INF_MAX_EA))

llm_input_data = {}

percorso_binario = idc.get_input_file_path() 

if 'bin_stripped/' in percorso_binario:
    rel_path = percorso_binario.split('bin_stripped/')[-1]
else:
    rel_path = os.path.basename(percorso_binario)

sub_dir = os.path.dirname(rel_path)
nome_base = os.path.splitext(os.path.basename(percorso_binario))[0]
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
output_dir = os.path.join(base_dir, 'data', 'llm_inputs', sub_dir)
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, f"{nome_base}.json")

for func in idautils.Functions():
    flags = idc.get_func_attr(func, idc.FUNCATTR_FLAGS)
    func_name_ida = idc.get_func_name(func)
    
    if (flags & idaapi.FUNC_LIB) or (flags & idaapi.FUNC_THUNK):
        continue

    try:
        cfunc = idaapi.decompile(func)
        if cfunc:
            pseudo_c_code = str(cfunc)
            
            variabili_correnti = {}
            for lvar in cfunc.get_lvars():
                if lvar.name and lvar.name != "retaddr":
                    variabili_correnti[lvar.name] = ""

            llm_input_data[hex(func)] = {
                "nome_corrente": func_name_ida,
                "codice_decompilato": pseudo_c_code,
                "variabili": variabili_correnti
            }
    except Exception:
        pass

with open(output_path, 'w') as f:
    json.dump(llm_input_data, f, indent=4)

print(f"extraction completed. data saved to: {output_path}")

if idaapi.cvar.batch:
    idc.qexit(0)