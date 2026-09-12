const form = document.getElementById("predictionForm");

const predictButton = document.getElementById("predictButton");

const loading = document.getElementById("loading");

const result = document.getElementById("result");

const errorBox = document.getElementById("error");

const prediction = document.getElementById("prediction");

const riskProbability =
    document.getElementById("riskProbability");

const recommendation =
    document.getElementById("recommendation");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Hide previous messages
    result.classList.add("hidden");
    errorBox.classList.add("hidden");

    // Show loading
    loading.classList.remove("hidden");

    predictButton.disabled = true;
    predictButton.textContent = "Analyzing...";


    const data = {

        study_hours:
            parseFloat(
                document.getElementById("study_hours").value
            ),

        attendance_percentage:
            parseFloat(
                document.getElementById(
                    "attendance_percentage"
                ).value
            ),

        previous_gpa:
            parseFloat(
                document.getElementById("previous_gpa").value
            ),

        parental_education:
            document.getElementById(
                "parental_education"
            ).value

    };


    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)

        });


        const resultData = await response.json();


        if (!resultData.success) {

            throw new Error(
                resultData.error ||
                "Prediction failed."
            );

        }


        // Display prediction
        prediction.textContent =
            "Prediction: " + resultData.prediction;


        riskProbability.textContent =
            resultData.risk_probability + "%";


        recommendation.textContent =
            resultData.recommendation;


        // Remove previous styling
        result.classList.remove(
            "safe",
            "risk"
        );


        // Apply result styling
        if (resultData.prediction === "AT RISK") {

            result.classList.add("risk");

        } else {

            result.classList.add("safe");

        }


        result.classList.remove("hidden");

    }

    catch (error) {

        errorBox.textContent =
            error.message;

        errorBox.classList.remove("hidden");

    }

    finally {

        loading.classList.add("hidden");

        predictButton.disabled = false;

        predictButton.textContent =
            "Predict Dropout Risk";

    }

});