import { AthenaClient, StartQueryExecutionCommand, GetQueryExecutionCommand, GetQueryResultsCommand } from '@aws-sdk/client-athena';
import { awsConfig } from '../config/aws-config';

class AthenaService {
  constructor() {
    this.client = new AthenaClient({
      region: awsConfig.region,
      credentials: awsConfig.credentials
    });
  }

  async executeQuery(queryString) {
    try {
      const startParams = {
        QueryString: queryString,
        QueryExecutionContext: {
          Database: awsConfig.athena.database
        },
        ResultConfiguration: {
          OutputLocation: awsConfig.athena.outputLocation
        },
        WorkGroup: awsConfig.athena.workGroup
      };

      const startCommand = new StartQueryExecutionCommand(startParams);
      const startResult = await this.client.send(startCommand);
      const queryExecutionId = startResult.QueryExecutionId;

      await this.waitForQueryCompletion(queryExecutionId);

      const resultsParams = {
        QueryExecutionId: queryExecutionId
      };

      const resultsCommand = new GetQueryResultsCommand(resultsParams);
      const resultsResponse = await this.client.send(resultsCommand);

      return this.formatResults(resultsResponse.ResultSet);

    } catch (error) {
      console.error('Error executing Athena query:', error);
      throw error;
    }
  }

  async waitForQueryCompletion(queryExecutionId, maxWaitTime = 30000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < maxWaitTime) {
      const params = {
        QueryExecutionId: queryExecutionId
      };

      const command = new GetQueryExecutionCommand(params);
      const result = await this.client.send(command);
      const status = result.QueryExecution.Status.State;

      if (status === 'SUCCEEDED') {
        return;
      } else if (status === 'FAILED' || status === 'CANCELLED') {
        throw new Error(`Query ${status}: ${result.QueryExecution.Status.StateChangeReason}`);
      }

      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    throw new Error('Query execution timed out');
  }

  formatResults(resultSet) {
    if (!resultSet || !resultSet.Rows || resultSet.Rows.length === 0) {
      return { columns: [], rows: [] };
    }

    const columns = resultSet.Rows[0].Data.map(col => col.VarCharValue || '');
    const rows = resultSet.Rows.slice(1).map(row => 
      row.Data.map(cell => cell.VarCharValue || '')
    );

    return { columns, rows };
  }
}

const athenaServiceInstance = new AthenaService();
export default athenaServiceInstance;