async function loadDashboard() {

    try {

        const response =
            await fetch("/api/dashboard");

        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error ||
                "Unable to load dashboard."
            );

        }


        // -----------------------------------------
        // SUMMARY
        // -----------------------------------------

        const summary =
            data.summary;


        document.getElementById(
            "totalStudents"
        ).textContent =
            summary.total_students;


        document.getElementById(
            "atRiskStudents"
        ).textContent =
            summary.at_risk_students;


        document.getElementById(
            "safeStudents"
        ).textContent =
            summary.safe_students;


        document.getElementById(
            "averageGpa"
        ).textContent =
            summary.average_gpa;


        document.getElementById(
            "averageAttendance"
        ).textContent =
            summary.average_attendance + "%";


        document.getElementById(
            "averageStudyHours"
        ).textContent =
            summary.average_study_hours;


        // -----------------------------------------
        // RISK DISTRIBUTION
        // -----------------------------------------

        document.getElementById(
            "atRiskPercentage"
        ).textContent =
            summary.at_risk_percentage + "%";


        document.getElementById(
            "safePercentage"
        ).textContent =
            summary.safe_percentage + "%";


        document.getElementById(
            "atRiskBar"
        ).style.width =
            summary.at_risk_percentage + "%";


        document.getElementById(
            "safeBar"
        ).style.width =
            summary.safe_percentage + "%";


        // -----------------------------------------
        // ACADEMIC COMPARISON
        // -----------------------------------------

        const comparison =
            data.academic_comparison;


        document.getElementById(
            "riskGpa"
        ).textContent =
            comparison.at_risk.average_gpa;


        document.getElementById(
            "riskAttendance"
        ).textContent =
            comparison.at_risk.average_attendance;


        document.getElementById(
            "riskStudyHours"
        ).textContent =
            comparison.at_risk.average_study_hours;


        document.getElementById(
            "safeGpa"
        ).textContent =
            comparison.safe.average_gpa;


        document.getElementById(
            "safeAttendance"
        ).textContent =
            comparison.safe.average_attendance;


        document.getElementById(
            "safeStudyHours"
        ).textContent =
            comparison.safe.average_study_hours;


        // -----------------------------------------
        // EDUCATION DISTRIBUTION
        // -----------------------------------------

        const education =
            data.education_distribution;


        const educationContainer =
            document.getElementById(
                "educationDistribution"
            );


        educationContainer.innerHTML = "";


        Object.entries(education).forEach(
            ([name, count]) => {

                const row =
                    document.createElement("div");

                row.className =
                    "education-row";


                row.innerHTML = `
                    <span>${name}</span>
                    <strong>${count}</strong>
                `;


                educationContainer.appendChild(
                    row
                );

            }
        );

    }

    catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


loadDashboard();
