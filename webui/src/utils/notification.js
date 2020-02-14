/* eslint-disable compat/compat */

export async function showNotification(title, options) {
  // Let's check if the browser supports notifications
  if (!('Notification' in window)) {
    return null;
  }

  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === 'granted') {
    // If it's okay let's create a notification
    return new Notification(title, options);
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then(function(permission) {
      // If the user accepts, let's create a notification
      if (permission === 'granted') {
        return new Notification(title, options);
      } else {
        return null;
      }
    });
  }

  return null;
}
