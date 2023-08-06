    
    wx.GridBlocks range = grid.GetSelectedBlocks()
    for (wx.GridBlocks.iterator it = range.begin()
          it != range.end()
          ++it) 
        ... do something with *it ...
