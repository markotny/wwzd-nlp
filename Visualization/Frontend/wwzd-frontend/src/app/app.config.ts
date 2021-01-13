import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';
import { IAppConfig } from './core/interfaces/app-config.interface';

@Injectable()
export class AppConfig {
  static settings: IAppConfig;
  
  constructor(private http: HttpClient) {}

  load() {
    const jsonFile = `assets/config/config.${environment.name}.json`;

    return new Promise<void>((resolve, reject) => {
      this.http
        .get(jsonFile)
        .toPromise()
        .then((responseConfigs: IAppConfig) => {
          AppConfig.settings = responseConfigs;
        })
        .catch((response: any) => {
          reject(`Could not load file': ${JSON.stringify(response)}`);
        });
    });
  }
}
