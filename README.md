<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clockify Activities</title>
</head>
<body>
    <h1>Clockify Activities</h1>
    <div id="activities"></div>

    <script>
        fetch('activities.json')
            .then(response => response.json())
            .then(data => {
                const activitiesDiv = document.getElementById('activities');
                data.forEach(activity => {
                    const activityDiv = document.createElement('div');
                    activityDiv.innerHTML = `
                        <h2>${activity.state}</h2>
                        <p>Description: ${activity.description}</p>
                        <p>Project Duration: ${activity.project_duration}</p>
                        <p>Start Time: ${new Date(activity.epoch * 1000).toLocaleString()}</p>
                    `;
                    activitiesDiv.appendChild(activityDiv);
                });
            })
            .catch(error => console.error('Error fetching activities:', error));
    </script>
</body>
</html>
