            function submitChanges() {
                // Create message content
                var messageContent = "Settings have been updated.";
        
                // Create webhook payload
                var webhookPayload = {
                    "content": messageContent
                };
        
                // Send webhook
                fetch('https://discord.com/api/webhooks/1239341156630925362/hmOGGNdh44dgr-FdV9rWRBJXGRKQ8ztHaYEvdZrWJ4d3FbYbwKgWqs8d4nJF9kmszL2h', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(webhookPayload)
                }).then(function(response) {
                    if (response.ok) {
                        alert('Settings saved successfully!');
                    } else {
                        alert('Failed to save settings. Please try again later.');
                    }
                }).catch(function(error) {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again later.');
                });
            }
