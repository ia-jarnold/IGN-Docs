Actions
=======

.. grid:: 2

   .. grid-item-card::
      :link: http://192.168.153.128:5000/refresh
            
      .. div:: sd-text-center

        :octicon:`issue-reopened;1em;sd-text-info` Will refresh the docs from source and navigate to the index page. 

   .. grid-item-card::
      :link: http://192.168.153.128:5000/archive

      .. div:: sd-text-center

        :octicon:`file-zip;1em;sd-text-info` Will create a tar archive of the html docs.In a configured archive directory. Download the docs to the browser. Comes with all js/css/image resources. Open index.html in browser. 

.. grid:: 1

   .. don't judge me...
   
   .. grid-item-card::
      :text-align: left 

       * :octicon:`git-compare;1em;sd-text-info` Manage Links.
        * If Link ID does not exist will add the Link URL
        * If Link ID does exist will overwrite the Link URL
        * If Remove checkbox is selected. The Link ID and URL are removed from the docs.(should replace really)
        * View :ref:`Current Links`

      .. raw:: html
      
          <form action="http://192.168.153.128:5000/ulink" method="GET" class="sd-row sd-row-cols-6">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="text" name="id" aria-labelledby="search-documentation" value="" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="Link ID" style="width: 200px"/>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="text" name="link" aria-labelledby="search-documentation" value="" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="Link URL" style="width: 450px"/>
            &nbsp;&nbsp;&nbsp;
            <label style="width: 95px">Remove?</label>
            <input type="checkbox" name="remove_link" aria-labelledby="search-documentation" value="True" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"/ style="width: 20px;">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <input type="submit" value="Manage Link" class="sd-card" />
          </form>

