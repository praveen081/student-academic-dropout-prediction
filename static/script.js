// ============================================================
// STUDENT PREDICTION SCRIPT
// ============================================================

const form = document.getElementById("predictionForm");

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

const recommendation =
    document.getElementById("recommendation");


// ============================================================
// CHECK REQUIRED ELEMENTS
// ============================================================

if (!form) {

    console.error(
        "Prediction form was not found."
    );

}


// ============================================================
// FORM SUBMISSION
// ============================================================

if (form) {

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            // ------------------------------------------------
            // Hide previous messages
            // ------------------------------------------------

            if (result) {
                result.classList.add("hidden");
            }

            if (errorBox) {
                errorBox.classList.add("hidden");
            }


            // ------------------------------------------------
            // Show loading
            // ------------------------------------------------

            if (loading) {
                loading.classList.remove("hidden");
            }

            if (predictButton) {

                predictButton.disabled = true;

                predictButton.textContent =
                    "Analyzing...";
            }


            // ------------------------------------------------
            // Read form values
            // ------------------------------------------------

            const studyHoursElement =
                document.getElementById(
                    "study_hours"
                );

            const attendanceElement =
                document.getElementById(
                    "attendance_percentage"
                );

            const gpaElement =
                document.getElementById(
                    "previous_gpa"
                );

            const educationElement =
                document.getElementById(
                    "parental_education"
                );


            const data = {

                study_hours:
                    parseFloat(
                        studyHoursElement.value
                    ),

                attendance_percentage:
                    parseFloat(
                        attendanceElement.value
                    ),

                previous_gpa:
                    parseFloat(
                        gpaElement.value
                    ),

                parental_education:
                    educationElement.value
            };


            // ------------------------------------------------
            // Send request to FastAPI
            // ------------------------------------------------

            try {

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


                // ------------------------------------------------
                // Check backend response
                // ------------------------------------------------

                if (!resultData.success) {

                    throw new Error(
                        resultData.error ||
                        "Prediction failed."
                    );
                }


                // ------------------------------------------------
                // Display prediction
                // ------------------------------------------------

                if (prediction) {

                    prediction.textContent =
                        resultData.prediction;
                }


                // ------------------------------------------------
                // Display risk probability
                // ------------------------------------------------

                if (riskProbability) {

                    riskProbability.textContent =
                        `${resultData.risk_probability}%`;
                }


                // ------------------------------------------------
                // Display recommendations
                // ------------------------------------------------

                if (recommendation) {

                    if (
                        Array.isArray(
                            resultData.recommendations
                        )
                    ) {

                        recommendation.innerHTML =
                            resultData.recommendations
                                .map(
                                    item =>
                                        `<div>• ${item}</div>`
                                )
                                .join("");

                    } else {

                        recommendation.textContent =
                            resultData.recommendations ||
                            "Continue monitoring academic performance.";
                    }
                }


                // ------------------------------------------------
                // Remove previous styling
                // ------------------------------------------------

                if (result) {

                    result.classList.remove(
                        "safe",
                        "risk",
                        "medium"
                    );
                }


                // ------------------------------------------------
                // Apply prediction styling
                // ------------------------------------------------

                if (result) {

                    if (
                        resultData.prediction ===
                        "AT RISK"
                    ) {

                        result.classList.add(
                            "risk"
                        );

                    } else {

                        result.classList.add(
                            "safe"
                        );
                    }
                }


                // ------------------------------------------------
                // Show result
                // ------------------------------------------------

                if (result) {

                    result.classList.remove(
                        "hidden"
                    );
                }

            }

            catch (error) {

                console.error(
                    "Prediction error:",
                    error
                );


                if (errorBox) {

                    errorBox.textContent =
                        error.message;

                    errorBox.classList.remove(
                        "hidden"
                    );
                }
            }


            finally {

                // ------------------------------------------------
                // Hide loading
                // ------------------------------------------------

                if (loading) {

                    loading.classList.add(
                        "hidden"
                    );
                }


                // ------------------------------------------------
                // Reset button
                // ------------------------------------------------

                if (predictButton) {

                    predictButton.disabled =
                        false;

                    predictButton.textContent =
                        "Predict Dropout Risk";
                }
            }

        }
    );

}
