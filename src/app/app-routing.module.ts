import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OptionsDataComponent } from './options-data/options-data.component';


const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'home' },
  { path: 'data', component: OptionsDataComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
