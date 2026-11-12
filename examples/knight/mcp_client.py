import subprocess, json, sys, os
EXE=os.path.expanduser("~/.claude/mcp/pixel-mcp/pixel-mcp.exe")
class C:
    def __init__(s):
        s.p=subprocess.Popen([EXE],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL); s.i=0
        s.rpc("initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}})
        s._w({"jsonrpc":"2.0","method":"notifications/initialized"})
    def _w(s,o): s.p.stdin.write(json.dumps(o).encode()+b"\n"); s.p.stdin.flush()
    def rpc(s,m,params):
        s.i+=1; s._w({"jsonrpc":"2.0","id":s.i,"method":m,"params":params})
        while True:
            ln=s.p.stdout.readline()
            if not ln: raise SystemExit("server closed")
            try: r=json.loads(ln)
            except Exception: continue
            if r.get("id")==s.i: return r
    def call(s,n,a):
        r=s.rpc("tools/call",{"name":n,"arguments":a})
        if "error" in r: raise RuntimeError(f"{n}: {r['error']}")
        res=r["result"]; txt=" ".join(x.get("text","") for x in res.get("content",[]))
        if res.get("isError"): raise RuntimeError(f"{n}: {txt}")
        return txt
if __name__=="__main__":
    c=C(); r=c.rpc("tools/list",{})
    for t in r["result"]["tools"]:
        if t["name"] in sys.argv[1:]: print(t["name"],json.dumps(t["inputSchema"]))
    print(len(r["result"]["tools"]),"tools")
