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

    // Hide previous messages
    errorBox.style.display = "none";
    result.style.display = "none";

    // Show loading state
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


        // -----------------------------
        // Prediction
        // -----------------------------

        prediction.textContent = resultData.prediction;

        riskProbability.textContent =
            `${Number(resultData.risk_probability).toFixed(2)}%`;

        riskLevel.textContent = resultData.risk_level;


        // -----------------------------
        // Risk Factors
        // -----------------------------

        riskFactors.innerHTML = "";

        if (
            resultData.risk_factors &&
            resultData.risk_factors.length > 0
        ) {
            resultData.risk_factors.forEach(function (factor) {
                const li = document.createElement("li");
                li.textContent = factor;
                riskFactors.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "No significant risk factors identified.";
            riskFactors.appendChild(li);
        }


        // -----------------------------
        // Recommendations
        // -----------------------------

        recommendations.innerHTML = "";

        if (
            resultData.recommendations &&
            resultData.recommendations.length > 0
        ) {
            resultData.recommendations.forEach(function (recommendation) {
                const li = document.createElement("li");
                li.textContent = recommendation;
                recommendations.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "Continue maintaining good academic habits.";
            recommendations.appendChild(li);
        }


        // -----------------------------
        // Show result
        // -----------------------------

        result.style.display = "block";


        // Scroll to result
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
