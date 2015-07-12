# -*- coding: utf-8 -*- 
<%inherit file="layout.mako"/>

<h1> Record List </h1>




<table border="1">
<thead class="tableHeader">
<tr>
<th>Name</th>
<th>E-mail id</th>
<th>Phone Number</th>
</tr>
</thead>
<tbody data-bind="foreach: details, visible: details().length > 0">
<tr>
<td data-bind="text: name" />
<td data-bind="text: mailid" />
<td data-bind="text: phone" />
<td data-bind="click: $root.delete"><a href = "#">Delete</a></td>
</tr>
</tbody>
</table>
<p>
<a href="${request.route_url('new')}">Add a new record</a>
</p>
<script src='/static/knockout.js'></script>
<script src='/static/jquery.js'></script>

<script type="text/javascript" >
//Detail model
function Detail(data) {
  this.id = ko.observable(data.id);
  this.name = ko.observable(data.name);
  this.phone = ko.observable(data.phone);
  //this.mailid = ko.observable(data.mailid)
}
//View Model
function DetailViewModel() {
var self = this;

//collection of details
self.details = ko.observableArray([]);

var a = ${details | n};
self.details(a);

this.delete = function(detail){
  var delete_link = "delete/".concat(detail.id);
  $.post(
      delete_link,
      {'action' : 'delete', 'id' : detail['id']},
      function(response){
          
          //remove the currently selected detail from the array
          self.details.remove(detail);
      }
  );
};

}



ko.applyBindings(new DetailViewModel());
</script>


