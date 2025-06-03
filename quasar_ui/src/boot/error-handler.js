export default async ({ app }) => {
  app.config.errorHandler = (err, instance, info) => {
    console.error('Vue Error Handler:', err)
    console.warn('Component instance:', instance)
    console.info('Error Info:', info)
  }

  window.onerror = function (message, source, lineno, colno, error) {
    console.error('Global JS Error:', {
      message,
      source,
      lineno,
      colno,
      error
    })
  }

  window.onunhandledrejection = function (event) {
    console.error('Unhandled Promise Rejection:', {
      reason: event.reason  
    })
  }
}
