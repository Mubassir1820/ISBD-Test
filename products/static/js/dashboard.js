document.addEventListener('DOMContentLoaded', function () {
    fetch('http://127.0.0.1:8000/orders/')
      .then(response => response.json())
      .then(data => {
        document.getElementById('total-orders').innerText = data.length;
      })
      .catch(error => {
        console.error('Error loading orders:', error);
      });
  
    fetch('/api/payments/')
      .then(response => response.json())
      .then(data => {
        let total = 0;
        data.forEach(payment => {
          total += parseFloat(payment.amount || 0);
        });
        document.getElementById('total-payments').innerText = `₦${total.toFixed(2)}`;
      })
      .catch(error => {
        console.error('Error loading payments:', error);
      });
  });