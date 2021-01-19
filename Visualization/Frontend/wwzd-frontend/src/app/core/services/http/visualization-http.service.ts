import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AppConfig } from 'src/app/app.config';

@Injectable({
    providedIn: 'root'
})
export class VisualizationHttpService<T, V> {
  constructor(protected httpClient: HttpClient) { }
  baseRoute = 'http://localhost:105';

  public get(endpoint: any, params?: HttpParams): Observable<T> {
    return this.httpClient
      .get<T>(this.baseRoute + '/' + endpoint, { params })
      .pipe(
        map((out: T) => {
          return out;
        })
      );
  }

  public post(endpoint: any, model: V, headers?: HttpHeaders): Observable<T> {
    return this.httpClient
      .post<T>(this.baseRoute + '/' + endpoint, model, { headers })
      .pipe(
        map((out: T) => {
          return out;
        })
      );
  }
}
