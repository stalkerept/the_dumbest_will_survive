with open("t.md", encoding='utf-8') as file:
    sp = file.readlines()

for i in sp:
    n = i.split("|")
    with open(n[0].strip(),"w", encoding="utf-8") as f:
        k = n[1].split(",")       
        for item in k:
            f.write(f"[[{item.strip()}]], ")
        f.write("\n")
