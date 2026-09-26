const form =
    document.getElementById("predictionForm");

const predictButton =
    document.getElementById("predictButton");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorBox =
    document.getElementById("error");

const prediction =
    document.getElementById("prediction");

const riskProbability =
    document.getElementById("riskProbability");

const riskLevel =
    document.getElementById("riskLevel");

const riskFactors =
    document.getElementById("riskFactors");

const recommendations =
    document.getElementById("recommendations");


form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Hide previous messages
        result.classList.add("hidden");

        errorBox.classList.add("hidden");


        // Show loading
        loading.classList.remove("hidden");

        predictButton.disabled = true;

        predictButton.textContent =
            "Analyzing...";


        // Collect student data
        const data = {

            study_hours:
                parseFloat(
                    document.getElementById(
                        "study_hours"
                    ).value
                ),

            attendance_percentage:
                parseFloat(
                    document.getElementById(
                        "attendance_percentage"
                    ).value
                ),

            previous_gpa:
                parseFloat(
                    document.getElementById(
                        "previous_gpa"
                    ).value
                ),

            parental_education:
                document.getElementById(
                    "parental_education"
                ).value

        };


        try {

            // Send request to FastAPI
            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );


            const resultData =
                await response.json();


            // Check API result
            if (!resultData.success) {

                throw new Error(
                    resultData.error ||
                    "Prediction failed."
                );

            }


            // -----------------------------------------
            // PREDICTION
            // -----------------------------------------

            prediction.textContent =
                resultData.prediction;


            // -----------------------------------------
            // RISK SCORE
            // -----------------------------------------

            riskProbability.textContent =
                resultData.risk_probability + "%";


            // -----------------------------------------
            // RISK LEVEL
            // -----------------------------------------

            riskLevel.textContent =
                resultData.risk_level;


            // -----------------------------------------
            // CLEAR OLD FACTORS
            // -----------------------------------------

            riskFactors.innerHTML = "";


            // Add risk factors
            resultData.risk_factors.forEach(
                function (factor) {

                    const li =
                        document.createElement("li");

                    li.textContent = factor;

                    riskFactors.appendChild(li);

                }
            );


            // -----------------------------------------
            // CLEAR OLD RECOMMENDATIONS
            // -----------------------------------------

            recommendations.innerHTML = "";


            // Add recommendations
            resultData.recommendations.forEach(
                function (recommendation) {

                    const li =
                        document.createElement("li");

                    li.textContent =
                        recommendation;

                    recommendations.appendChild(li);

                }
            );


            // -----------------------------------------
            // RESULT STYLING
            // -----------------------------------------

            result.classList.remove(
                "safe",
                "risk",
                "medium"
            );


            if (
                resultData.risk_level === "HIGH"
            ) {

                result.classList.add("risk");

            }
            else if (
                resultData.risk_level === "MEDIUM"
            ) {

                result.classList.add("medium");

            }
            else {

                result.classList.add("safe");

            }


            // Show result
            result.classList.remove("hidden");

        }


        catch (error) {

            errorBox.textContent =
                error.message;

            errorBox.classList.remove(
                "hidden"
            );

        }


        finally {

            loading.classList.add("hidden");

            predictButton.disabled = false;

            predictButton.textContent =
                "Analyze Student Risk";

        }

    }
);
