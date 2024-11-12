document.getElementById('trafficForm').addEventListener("submit", async function(e) {
    e.preventDefault();

    const bikeCount = document.getElementById("bike_count").value;
    const carCount = document.getElementById("car_count").value;
    const roadWidth = document.getElementById("road_width").value;
    try {
        const resp = await fetch("/", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({
                bikeCount, carCount, roadWidth
            })
        });
    }
    catch(error){
        
    }

    const data = await resp.json();

    document.getElementById("duration").innerText = `${data.grnlght} seconds`;
});
