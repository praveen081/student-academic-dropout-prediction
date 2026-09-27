const form = document.getElementById("predictionForm");
const predictButton = document.getElementById("predictButton");

const loading = document.getElementById("loading");
const result = document.getElementById("result");
const errorBox = document.getElementById("error");

const prediction = document.getElementById("prediction");
const riskProbability = document.getElementById("riskProbability");
const riskLevel = document.getElementById("riskLevel");

const riskFactors = document.getElementById("riskFactors");
const recommendations = document.getElementById("recommendations");


form.addEventListener("submit", async function (event) {
    event.preventDefault();

    errorBox.style.display = "none";
    result.style.display = "none";

    loading.style.display = "block";
    predictButton.disabled = true;
    predictButton.textContent = "Analyzing...";

    const studyHours = Number(
        document.getElementById("study_hours").value
    );

    const attendancePercentage = Number(
        document.getElementById("attendance_percentage").value
    );

    const previousGpa = Number(
        document.getElementById("previous_gpa").value
    );

    const parentalEducation =
        document.getElementById("parental_education").value;


    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                study_hours: studyHours,
                attendance_percentage: attendancePercentage,
                previous_gpa: previousGpa,
                parental_education: parentalEducation
            })
        });


        const resultData = await response.json();


        if (!response.ok) {
            throw new Error(
                resultData.detail || "Prediction failed."
            );
        }


        // Prediction
        prediction.textContent = resultData.prediction;

        riskProbability.textContent =
            `${Number(resultData.risk_probability).toFixed(2)}%`;

        riskLevel.textContent = resultData.risk_level;


        // Display risk factors
        if (Array.isArray(resultData.risk_factors)) {
            riskFactors.innerHTML = resultData.risk_factors
                .map(factor => `<p>• ${factor}</p>`)
                .join("");
        } else {
            riskFactors.innerHTML =
                `<p>${resultData.risk_factors || "No major warning signs identified."}</p>`;
        }


        // Display recommendations
        if (Array.isArray(resultData.recommendations)) {
            recommendations.innerHTML = resultData.recommendations
                .map(item => `<p>• ${item}</p>`)
                .join("");
        } else {
            recommendations.innerHTML =
                `<p>${resultData.recommendations || "Continue maintaining good academic performance."}</p>`;
        }


        // Show result
        result.style.display = "block";

        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {

        errorBox.textContent =
            error.message || "Something went wrong.";

        errorBox.style.display = "block";

    } finally {

        loading.style.display = "none";

        predictButton.disabled = false;
        predictButton.textContent = "Analyze Student Risk";
    }
});
