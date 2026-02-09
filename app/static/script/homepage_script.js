        
let index = 0;
const slides = document.querySelector(".slides");
const total = document.querySelectorAll(".slides img").length+1;

document.querySelectorAll(".fav-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const productId = this.dataset.id;
        const button = this;

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
            }
        });
    });
});

function showSlide() {
    if(index>=total-1) { index=0; }
    if(index<0) { index=total-1; }
    slides.style.transform = `translateX(-${index * 100}%)`;
}

document.querySelector(".next").onclick = () => {
    index++;
    showSlide();
}

document.querySelector(".prev").onclick = () => {
    index--;
    showSlide();
}

// Auto Slide Every 3 Seconds
setInterval(()=>{
    index++;
    showSlide();
},3500);