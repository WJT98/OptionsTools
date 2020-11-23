import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';

import {API_URL} from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class OptionsApiService {

  constructor(private http: HttpClient) {
  }


  // GET list of public, future events
  getOptions() {
    return this.http.get(`${API_URL}/tickers`);
	}


}