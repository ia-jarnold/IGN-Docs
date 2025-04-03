Actions
#######


.. grid:: 2

   .. grid-item-card::
      :link: http://192.168.153.128:5000/refresh
            
      .. div:: sd-text-center

        :octicon:`issue-reopened;1em;sd-text-info` Will refresh the docs from source and navigate to the index page. 


   .. grid-item-card::
      :link: http://192.168.153.128:5000/archive

      .. div:: sd-text-center

        :octicon:`file-zip;1em;sd-text-info` Will create a tar archive of the html docs in a configured archive directory. 

.. grid:: 1

   .. grid-item-card::

      | Add and or update links

      .. raw:: html
      
          <form action="http://192.168.153.128:5000/ulink" method="GET">
            <input type="text" name="id" aria-labelledby="search-documentation" value="" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"/>
            <input type="text" name="link" aria-labelledby="search-documentation" value="" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"/>
            <input type="submit" value="Update/Add" />
            <!--<span id="search-progress" style="padding-left: 10px"></span>-->
          </form>

