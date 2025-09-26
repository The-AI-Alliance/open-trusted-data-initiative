export const awsConfig = {
  region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
    sessionToken: process.env.REACT_APP_AWS_SESSION_TOKEN
  },
  athena: {
    database: process.env.REACT_APP_ATHENA_DATABASE || 'default',
    outputLocation: process.env.REACT_APP_ATHENA_OUTPUT_LOCATION || 's3://your-athena-results-bucket/',
    workGroup: process.env.REACT_APP_ATHENA_WORKGROUP || 'primary'
  }
};