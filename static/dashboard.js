document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    loadModelPerformance();
});


// ============================================================
// LOAD DASHBOARD DATA
// ============================================================

async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        const data = await response.json();

        if (!data.success) {
            throw new Error(
                data.error || "Unable to load dashboard data."
            );
        }

        updateSummary(data.summary);

        updateRiskDistribution(
            data.summary
        );

        updateAcademicComparison(
            data.academic_comparison
        );

        updateEducationDistribution(
            data.education_distribution
        );

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

        showDashboardError(
            error.message
        );
    }
}


// ============================================================
// UPDATE SUMMARY CARDS
// ============================================================

function updateSummary(summary) {

    setText(
        "totalStudents",
        summary.total_students
    );

    setText(
        "atRiskStudents",
        summary.at_risk_students
    );

    setText(
        "safeStudents",
        summary.safe_students
    );

    setText(
        "averageGpa",
        summary.average_gpa
    );

    setText(
        "averageAttendance",
        `${summary.average_attendance}%`
    );

    setText(
        "averageStudyHours",
        `${summary.average_study_hours} hrs`
    );
}


// ============================================================
// RISK DISTRIBUTION
// ============================================================

function updateRiskDistribution(summary) {

    setText(
        "atRiskPercentage",
        `${summary.at_risk_percentage}%`
    );

    setText(
        "safePercentage",
        `${summary.safe_percentage}%`
    );


    const atRiskBar =
        document.getElementById(
            "atRiskBar"
        );

    const safeBar =
        document.getElementById(
            "safeBar"
        );


    if (atRiskBar) {

        atRiskBar.style.width =
            `${summary.at_risk_percentage}%`;
    }


    if (safeBar) {

        safeBar.style.width =
            `${summary.safe_percentage}%`;
    }
}


// ============================================================
// ACADEMIC COMPARISON
// ============================================================

function updateAcademicComparison(
    comparison
) {

    const atRisk =
        comparison.at_risk;

    const safe =
        comparison.safe;


    setText(
        "riskGpa",
        atRisk.average_gpa
    );

    setText(
        "riskAttendance",
        `${atRisk.average_attendance}%`
    );

    setText(
        "riskStudyHours",
        `${atRisk.average_study_hours} hrs`
    );


    setText(
        "safeGpa",
        safe.average_gpa
    );

    setText(
        "safeAttendance",
        `${safe.average_attendance}%`
    );

    setText(
        "safeStudyHours",
        `${safe.average_study_hours} hrs`
    );
}


// ============================================================
// EDUCATION DISTRIBUTION
// ============================================================

function updateEducationDistribution(
    distribution
) {

    const container =
        document.getElementById(
            "educationDistribution"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    const entries =
        Object.entries(
            distribution
        );


    if (entries.length === 0) {

        container.innerHTML =
            "<p>No education data available.</p>";

        return;
    }


    entries.forEach(
        ([education, count]) => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "education-item";


            const label =
                document.createElement(
                    "span"
                );

            label.textContent =
                education;


            const value =
                document.createElement(
                    "strong"
                );

            value.textContent =
                count;


            item.appendChild(
                label
            );

            item.appendChild(
                value
            );


            container.appendChild(
                item
            );
        }
    );
}


// ============================================================
// LOAD MODEL PERFORMANCE
// ============================================================

async function loadModelPerformance() {

    const container =
        document.getElementById(
            "modelPerformance"
        );


    if (!container) {
        return;
    }


    try {

        const response =
            await fetch(
                "/api/model-performance"
            );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.message ||
                "Model performance data is unavailable."
            );
        }


        renderModelPerformance(
            data.models
        );

    } catch (error) {

        console.error(
            "Model performance error:",
            error
        );


        container.innerHTML = `
            <div class="dashboard-error">
                <p>
                    Model performance is not available yet.
                </p>

                <small>
                    Run train_model.py to generate
                    model_comparison.json.
                </small>
            </div>
        `;
    }
}


// ============================================================
// RENDER MODEL PERFORMANCE
// ============================================================

function renderModelPerformance(
    models
) {

    const container =
        document.getElementById(
            "modelPerformance"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    Object.entries(
        models
    ).forEach(
        ([modelName, metrics]) => {

            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "model-performance-card";


            card.innerHTML = `

                <div class="model-card-header">

                    <h3>
                        ${modelName}
                    </h3>

                </div>


                <div class="model-metrics-grid">


                    <div class="model-metric">

                        <span>
                            Accuracy
                        </span>

                        <strong>
                            ${formatPercent(
                                metrics.accuracy
                            )}
                        </strong>

                    </div>


                    <div class="model-metric">

                        <span>
                            At-Risk Precision
                        </span>

                        <strong>
                            ${formatPercent(
                                metrics.precision
                            )}
                        </strong>

                    </div>


                    <div class="model-metric">

                        <span>
                            At-Risk Recall
                        </span>

                        <strong>
                            ${formatPercent(
                                metrics.recall
                            )}
                        </strong>

                    </div>


                    <div class="model-metric">

                        <span>
                            At-Risk F1
                        </span>

                        <strong>
                            ${formatPercent(
                                metrics.f1
                            )}
                        </strong>

                    </div>


                    <div class="model-metric">

                        <span>
                            ROC-AUC
                        </span>

                        <strong>
                            ${formatNumber(
                                metrics.roc_auc
                            )}
                        </strong>

                    </div>


                    <div class="model-metric">

                        <span>
                            5-Fold CV F1
                        </span>

                        <strong>
                            ${formatNumber(
                                metrics.cv_f1_mean
                            )}
                        </strong>

                    </div>


                </div>


                <p class="cv-description">

                    Cross-validation variation:
                    ±${formatNumber(
                        metrics.cv_f1_std
                    )}

                </p>

            `;


            container.appendChild(
                card
            );
        }
    );
}


// ============================================================
// FORMAT HELPERS
// ============================================================

function formatPercent(
    value
) {

    return `${(
        Number(value) * 100
    ).toFixed(2)}%`;
}


function formatNumber(
    value
) {

    return Number(value).toFixed(4);
}


function setText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (element) {

        element.textContent =
            value;
    }
}


// ============================================================
// ERROR DISPLAY
// ============================================================

function showDashboardError(
    message
) {

    const container =
        document.querySelector(
            ".dashboard-container"
        );


    if (!container) {
        return;
    }


    const error =
        document.createElement(
            "div"
        );


    error.className =
        "dashboard-error";


    error.innerHTML = `
        <strong>
            Dashboard data could not be loaded.
        </strong>

        <p>
            ${message}
        </p>
    `;


    container.prepend(
        error
    );
}
