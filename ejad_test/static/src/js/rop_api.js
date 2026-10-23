(function () {
    function start() {
        const button = document.getElementById("rop_api_load");
        if (!button) {
            return;
        }
        button.addEventListener("click", async () => {
            const status = document.getElementById("rop_api_status");
            const response = await fetch("/rop-product");
            if (!response.ok) {
                status.textContent = "Request failed (" + response.status + ")";
                return;
            }
            const products = await response.json();
            status.textContent = products.length + " product(s) loaded";
            document.getElementById("rop_api_body").replaceChildren(...products.map((product) => {
                const row = document.createElement("tr");
                for (const value of [product.id, product.name, product.qty]) {
                    const cell = document.createElement("td");
                    cell.textContent = value;
                    row.appendChild(cell);
                }
                return row;
            }));
        });
    }
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
