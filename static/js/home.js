function checkCompliance() {
    const urlInput = document.getElementById('url');
    const policyUrlInput = document.getElementById('policy_url');
    const findingsDiv = document.getElementById('findings');

    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        findingsDiv.innerHTML = '';      
        $.ajax({
            type: 'POST',
            url: '/scrape_and_compare/',
            data: {
                url: urlInput.value,
                policy_url: policyUrlInput.value
            },
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') 
            },
            success: function (data) {
                findingsDiv.textContent = data.findings;
                alert('Successful');
            },
            error: function () {
                console.error('Error: Request failed');
                findingsDiv.textContent = 'Error: Request failed';
                alert('Failure');
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

document.addEventListener('DOMContentLoaded', checkCompliance);
