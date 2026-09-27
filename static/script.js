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

    // Show loading
    loading.style.display = "block";
    predictButton.disabled = true;
    predictButton.textContent = "Analyzing...";


    // Get form values
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

        // Send prediction request
        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                study_hours: studyHours,

                attendance_percentage:
                    attendancePercentage,

                previous_gpa:
                    previousGpa,

                parental_education:
                    parentalEducation
            })
        });


        // Convert response to JSON
        const resultData = await response.json();


        // Check API response
        if (!response.ok) {

            throw new Error(
                resultData.detail ||
                resultData.error ||
                "Prediction failed."
            );
        }


        // =========================================
        // DISPLAY PREDICTION
        // =========================================

        prediction.textContent =
            resultData.prediction;


        // =========================================
        // DISPLAY RISK PROBABILITY
        // =========================================

        riskProbability.textContent =
            `${Number(resultData.risk_probability).toFixed(2)}%`;


        // =========================================
        // DISPLAY RISK LEVEL
        // =========================================

        riskLevel.textContent =
            resultData.risk_level;


        // =========================================
        // DISPLAY RISK FACTORS
        // =========================================

        riskFactors.innerHTML = "";


        if (
            Array.isArray(resultData.risk_factors)
        ) {

            resultData.risk_factors.forEach(
                function (factor) {

                    const li =
                        document.createElement("li");

                    li.textContent = factor;

                    riskFactors.appendChild(li);
                }
            );

        } else {

            const li =
                document.createElement("li");

            li.textContent =
                resultData.risk_factors ||
                "No major warning signs identified.";

            riskFactors.appendChild(li);
        }


        // =========================================
        // DISPLAY RECOMMENDATIONS
        // =========================================

        recommendations.innerHTML = "";


        if (
            Array.isArray(resultData.recommendations)
        ) {

            resultData.recommendations.forEach(
                function (recommendation) {

                    const li =
                        document.createElement("li");

                    li.textContent = recommendation;

                    recommendations.appendChild(li);
                }
            );

        } else {

            const li =
                document.createElement("li");

            li.textContent =
                resultData.recommendations ||
                "Continue maintaining good academic performance.";

            recommendations.appendChild(li);
        }


        // =========================================
        // SHOW RESULT
        // =========================================

        result.style.display = "block";


        // Scroll to result
        result.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    } catch (error) {

        // Display error
        errorBox.textContent =
            error.message ||
            "Something went wrong.";

        errorBox.style.display = "block";


    } finally {

        // Hide loading
        loading.style.display = "none";


        // Reset button
        predictButton.disabled = false;

        predictButton.textContent =
            "Analyze Student Risk";
    }

});
