============
General Docs
============

* `Basic Time Complexity`_

  * Good examples
  * Sort is n^2 in unsorted list since each list element has to check each other. [2,3,1] -> len 3 ->

    * 2,2 : 2,3 : 2,1 
    * 3,2 : 3,3 : 3,1
    * 1,2 : 1,3 : 1,1 -> 9 checks/compare ops -> 3^2 -> len(list)^2 -> n2
    * my basic retention example

  * But really Big-O means worst case in terms of resource. And If an algorithm handles the worst case all others will work.
    
    * See Basic Induction (no pun)
    * https://en.wikipedia.org/wiki/Mathematical_induction
    * Requriements -> Worst Case -> code once -> get rest for free.
    * Requirements -> Base Case  -> Scale/iterate from there appropreatly.

      * may not have all resources for worst case but how close can we get with base case, a single python process for instance.

