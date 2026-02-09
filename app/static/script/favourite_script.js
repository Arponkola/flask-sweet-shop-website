document.querySelectorAll(".fav-btn").forEach(btn => {
    btn.addEventListener("click", function () {
    const productId = this.dataset.id;
    const button = this;
    const divToRemove = button.closest('.card')
        divToRemove.classList.add('removing')

    fetch(`/add-to-favourite/${productId}`, { method: "POST" })
        .then(res => res.json())
        .then(data => {

            if (data.redirect) {
                window.location.href = "/login";
                return;
            }

            if (data.success) {
                // Update navbar count
                document.getElementById("fav-count").innerText = data.count;

                        // Toggle heart color
                if (data.action === "added") {
                    button.classList.remove("btn-outline-danger");
                    button.classList.add("btn-danger");
                } else {
                    button.classList.remove("btn-danger");
                    button.classList.add("btn-outline-danger");
                }

                        //remove the cart
                        //divToRemove.style.opacity = '0';
                        //divToRemove.style.transition = 'opacity 1s ease';

                divToRemove.addEventListener('transitionend', () => {
                divToRemove.remove();
                }, { once: true });
            }
        });
    });
});