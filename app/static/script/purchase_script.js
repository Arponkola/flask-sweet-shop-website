function addRow() {
    const table = document.querySelector("#cartTable tbody");
    const row = document.createElement("tr");

    let options = "";
    PRODUCTS.forEach(p => {
        options += `
            <option value="${p.id}" data-price="${p.price}" data-stock="${p.stock}">
                ${p.name}
            </option>
        `;
    });

    row.innerHTML = `
        <td>
            <select class="form-select product" name="product_id[]" onchange="updateRow(this)">
                ${options}
            </select>
        </td>
        <td class="stock">0</td>
        <td class="price">0</td>
        <td>
            <input type="number" class="form-control qty" name="qty[]"
                   min="1" value="1" oninput="calculateRow(this)">
        </td>
        <td class="rowTotal">0</td>
        <td class="text-center">
            <span class="remove" onclick="removeRow(this)">✖</span>
        </td>
    `;

    table.appendChild(row);
}


function updateRow(select) {
    const option = select.selectedOptions[0];
    const row = select.closest("tr");

    row.querySelector(".price").innerText = option.dataset.price;
    row.querySelector(".stock").innerText = option.dataset.stock;

    const qty = row.querySelector(".qty");
    qty.max = option.dataset.stock;
    qty.value = 1;

    calculateRow(qty);
}

function calculateRow(input) {
    const row = input.closest("tr");
    const price = Number(row.querySelector(".price").innerText);
    const qty = Number(input.value);
    row.querySelector(".rowTotal").innerText = price * qty;
    calculateGrandTotal();
}

function calculateGrandTotal() {
    let total = 0;
    document.querySelectorAll(".rowTotal").forEach(r => {
        total += Number(r.innerText);
    });
    document.getElementById("grandTotal").innerText = total;
}

function removeRow(btn) {
    btn.closest("tr").remove();
    calculateGrandTotal();
}

// initial calc
calculateRow(document.querySelector(".qty"));