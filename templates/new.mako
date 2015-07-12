# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1>Add a new record</h1>

<form action="${request.route_url('new')}" method="post">
  Name:<input type="text" maxlength="100" name="name"><br/>
  Mail-ID:<input type="text" maxlength="100" name="mailid"><br/>
  Phone:<input type="text" maxlength="10" name="phone"></br>
  <input type="submit" name="add" value="ADD" class="button">
</form>