export interface IAppConfig {
    env: {
      name: string;
      production: boolean;
      platform: string;
    };
    httpOptions: {
      getRetryCount: 0;
      postRetryCount: 0;
      deleteRetryCount: 0;
      updateRetryCount: 0;
    };
    baseUrl: string;
  }