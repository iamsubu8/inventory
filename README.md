# inventory
### Installation
Technology-

Programming Language - Python
Framework - Django
Database -SQLite
Frontend- HTML,CSS,Javascript

1. Clone the repository:

    ```cmd
    git clone https://github.com/iamsubu8/inventory.git
    ```

2. Navigate to the project directory:

    ```cmd
    cd vms_project
    ```

3. Install dependencies:

    ```cmd
    pip install -r requirements.txt
    ```

4. Run the development server:

    ```cmd
    python manage.py runserver
    ```

The application should now be accessible at `http://127.0.0.1:8000/`.


User- Store Manager -
    username- store
    password-123qwe..

User- Deparment Manager-
    username-department
    password-123qwe..

login -http://127.0.0.1:8000/
To fetch all product - http://127.0.0.1:8000/productList
To fetch all pending products -http://127.0.0.1:8000/pending


### API
# 1./login:
This endpoint is used for user authentication.
    Method: POST
    Parameters:
        username: The username of the user.
        password: The password of the user.
    Returns:
        If the authentication is successful, it returns a JWT access token.
        If the authentication fails, it returns an error message.

# 2.POST /api/products:
This endpoint is used to add a new product.
    Method: POST
    Parameters:
        product_id: The ID of the product.
        product_name: The name of the product.
        vendor: The vendor of the product.
        mrp: The Maximum Retail Price (MRP) of the product.
        batch_number: The batch number of the product.
        batch_date: The batch date of the product.
        quantity: The quantity of the product.
    Returns:
        If the user has the 'store' role, it adds the product and returns a success message.
        If the user has the 'dprt' role, it sends the product for approval and returns a success message.
        If the user doesn't have permission, it returns an error message.

# 3.GET /api/products:
This endpoint is used to retrieve approved products.
    Method: GET
    Returns:
        If the user has the 'store' or 'dprt' role, it returns a list of approved products.
        If the user doesn't have permission, it returns an error message.

# 4.PUT /api/products:
This endpoint is used to update a product.
    Method: PUT
    Parameters:
        product_id: The ID of the product to be updated.
        Other parameters are similar to the ones in the POST method.
    Returns:
        If the user has the 'store' role, it updates the product and returns a success message.
        If the user has the 'dprt' role, it sends the updated product for approval and returns a success message.
        If the user doesn't have permission, it returns an error message.

# 5.DELETE /api/products:
This endpoint is used to delete a product.
    Method: DELETE
    Parameters:
        product_id: The ID of the product to be deleted.
    Returns:
        If the user has the 'store' role, it deletes the product and returns a success message.
        If the user has the 'dprt' role, it sends the product deletion request for approval and returns a success message.
        If the user doesn't have permission, it returns an error message.

# 6.GET /api/pendingProducts:
This endpoint is used to retrieve pending product requests.
    Method: GET
    Returns:
        If the user has the 'store' or 'dprt' role, it returns a list of pending product requests.
        If the user doesn't have permission, it returns an error message.

# 7.POST /api/aprove/<recored_id>:
This endpoint is used to approve a pending product request.
    Method: POST
    Parameters:
        recored_id: The ID of the pending product request to be approved.
    Returns:
        If the user has the 'store' role, it approves the product request and returns a success message.
        If the user doesn't have permission, it returns an error message.

# 8.POST /api/reject/<recored_id>:
This endpoint is used to reject a pending product request.
    Method: POST
    Parameters:
        recored_id: The ID of the pending product request to be rejected.
    Returns:
        If the user has the 'store' role, it rejects the product request and returns a success message.
        If the user doesn't have permission, it returns an error message.
