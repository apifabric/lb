import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductHomeComponent } from './home/Product-home.component';
import { ProductNewComponent } from './new/Product-new.component';
import { ProductDetailComponent } from './detail/Product-detail.component';

const routes: Routes = [
  {path: '', component: ProductHomeComponent},
  { path: 'new', component: ProductNewComponent },
  { path: ':id', component: ProductDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Product-detail-permissions'
      }
    }
  },{
    path: ':product_id/Inventory', loadChildren: () => import('../Inventory/Inventory.module').then(m => m.InventoryModule),
    data: {
        oPermission: {
            permissionId: 'Inventory-detail-permissions'
        }
    }
},{
    path: ':product_id/OrderItem', loadChildren: () => import('../OrderItem/OrderItem.module').then(m => m.OrderItemModule),
    data: {
        oPermission: {
            permissionId: 'OrderItem-detail-permissions'
        }
    }
},{
    path: ':product_id/ProductCategory', loadChildren: () => import('../ProductCategory/ProductCategory.module').then(m => m.ProductCategoryModule),
    data: {
        oPermission: {
            permissionId: 'ProductCategory-detail-permissions'
        }
    }
},{
    path: ':product_id/Review', loadChildren: () => import('../Review/Review.module').then(m => m.ReviewModule),
    data: {
        oPermission: {
            permissionId: 'Review-detail-permissions'
        }
    }
},{
    path: ':product_id/SupplierProduct', loadChildren: () => import('../SupplierProduct/SupplierProduct.module').then(m => m.SupplierProductModule),
    data: {
        oPermission: {
            permissionId: 'SupplierProduct-detail-permissions'
        }
    }
}
];

export const PRODUCT_MODULE_DECLARATIONS = [
    ProductHomeComponent,
    ProductNewComponent,
    ProductDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductRoutingModule { }