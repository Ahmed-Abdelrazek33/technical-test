(function () {
    function start() {
        const body = document.getElementById("rop_realtime_body");
        if (!body) {
            return;
        }
        async function refresh() {
            const response = await fetch("/rop/realtime/data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ jsonrpc: "2.0", method: "call", params: {} }),
            });
            const products = (await response.json()).result || [];
            document.getElementById("rop_realtime_count").textContent = products.length;
            body.replaceChildren(...products.map((product) => {
                const row = document.createElement("tr");
                for (const value of [product.name, product.qty]) {
                    const cell = document.createElement("td");
                    cell.textContent = value;
                    row.appendChild(cell);
                }
                return row;
            }));
        }
        refresh();
        setInterval(refresh, 3000);
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
