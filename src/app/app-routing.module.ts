import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { GammaExposureComponent } from './gamma-exposure/gamma-exposure.component';
import { DashboardComponent } from './dashboard/dashboard.component';


const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  { path: 'dashboard', component: DashboardComponent},
  { path: 'data', component: GammaExposureComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
