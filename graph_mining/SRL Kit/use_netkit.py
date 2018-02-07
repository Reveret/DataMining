import subprocess
from os import path

execute = ["java", "-jar", "netkit-srl-1.3.0/lib/NetKit-1.3.0.jar"]
files = [
    "imdb/imdb_all/imdb_all.arff",
    "imdb/imdb_prodco/imdb_prodco.arff",
    "cora/cora_all/cora_all.arff",
    "cora/cora_cite/cora_cite.arff"]
for f in ["cornell", "texas", "wisconsin"]:
    files.append("webkb/webkb_{}_cocite/WebKB-{}-cocite.arff".format(f, f))
    files.append("webkb/webkb_{}_link1/WebKB-{}-link1.arff".format(f, f))

for f in files:
    p = r"""C:/Users/jonas/Documents/"Uni Mainz Studium"/"Data Mining WiSe2017-18"/github/graph_mining/"SRL Kit"/"""
    out = r"output/" + path.basename(f).split(".")[0]
    subprocess.run(execute + ["-showauc"] + ["-output", out] + [f], shell=True)

print("-"*20)
print("Finished")
while True: pass
