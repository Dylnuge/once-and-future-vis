// Generated by CoffeeScript 1.7.1
(function() {
  var add_circle, colors, gen_word_plot, get_range_value, height, max_cx, max_cy, max_radius, min_cx, min_cy, min_radius, plot, random_color, width;

  colors = ["#C33048", "#276168", "#FDCD8D", "#AD705B", "#EB5057"];

  width = 1000;

  height = 650;

  min_radius = 20;

  max_radius = 100;

  min_cx = 100;

  min_cy = 100;

  max_cx = 960;

  max_cy = 550;

  random_color = function() {
    return colors[Math.floor(Math.random() * colors.length)];
  };

  plot = d3.select("#vis").append("svg").attr("width", width).attr("height", height);

  add_circle = function(cx, cy, r, label) {
    plot.append("circle").style("fill", random_color()).style("stroke", "gray").attr("cx", cx).attr("cy", cy).attr("r", r).on("mouseover", function() {
      return d3.select(this).style("fill", random_color());
    }).on("mouseout", function() {
      return d3.select(this).style("fill", random_color());
    }).on("click", function() {
      return d3.select("#selected-item").text("Selected word: " + label);
    }).append("svg:title").text(label);
    return plot.append("svg:text").text(label).attr("text-anchor", "middle").attr("x", cx).attr("y", cy);
  };

  get_range_value = function(min, max, percent) {
    return min + (percent * (max - min));
  };

  gen_word_plot = function(word_list, x_start, size) {
    var max_chap_x, min_chap_x, word, _i, _len, _results;
    min_chap_x = x_start;
    max_chap_x = x_start + size;
    _results = [];
    for (_i = 0, _len = word_list.length; _i < _len; _i++) {
      word = word_list[_i];
      _results.push(add_circle(get_range_value(min_chap_x, max_chap_x, word.pos), get_range_value(min_cy, max_cy, 1 - word.uniqueness), get_range_value(min_radius, max_radius, word.freq), word.word));
    }
    return _results;
  };

  d3.json("data/vis.json", function(error, json) {
    var chapter, chapter_size, chapters, i, _i, _len, _results;
    if (error) {
      return console.warn(error);
    }
    chapters = json;
    chapter_size = (max_cx - min_cx) / chapters.length;
    _results = [];
    for (i = _i = 0, _len = chapters.length; _i < _len; i = ++_i) {
      chapter = chapters[i];
      _results.push(gen_word_plot(chapter, min_cx + (i * chapter_size), chapter_size));
    }
    return _results;
  });

}).call(this);
