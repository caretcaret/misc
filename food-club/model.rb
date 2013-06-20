#!/usr/bin/ruby
# coding: utf-8

require 'sqlite3'
require 'matrix'
require './softmax_regression'
require './preprocessor'

def load_data(db)
  data = []
  db.execute "SELECT * FROM arenas" do |row|
    data << row
  end
  data
end

class Data
  attr_accessor :train_x, :train_y, :xvalid_x, :xvalid_y, :test_x, :test_y
  attr_reader :input_dim, :output_dim
  def initialize(classification, input_dim, output_dim=1)
    @classification = classification
    @input_dim = input_dim
    @output_dim = output_dim
  end
end

class ModifiedSoftmax
  attr_accessor :parameters, :norm_weight, :xs, :ys
  def initialize(xs, ys, norm_weight=0, parameters=nil)
    # assumption: parameters are the same for each class, since the
    # contest is symmetrical.
    if parameters.nil?
      @parameters = Vector[*Array.new(24){rand - 0.5}]
    else
      @parameters = parameters
    end
    @norm_weight = norm_weight
    @xs = xs
    @ys = ys
  end

  def hypothesis(parameters, x)
    log_hypothesis(parameters, x).map do |log_component|
      Math.exp(log_component)
    end
  end

  def get_pirates(x)
    arena = x.to_a
    pirates = [arena[0..22], arena[23..45], arena[46..68], arena[69..91]]
    pirates.map { |pirate| Vector[*pirate.unshift(1)] }
  end

  def log_hypothesis(parameters, x)
    pirates = get_pirates(x)
    log_zs = pirates.map { |pirate| pirate.inner_product(parameters) }
    # normalize
    z_max = log_zs.max
    sum = 0.0
    log_zs.each do |log_z|
      sum += Math.exp(log_z - z_max)
    end
    log_sum = z_max + Math.log(sum)
    log_probabilities = log_zs.map { |log_z| log_z - log_sum }
    Vector[*log_probabilities]
  end

  def predict(x)
    res = log_hypothesis(@parameters, x)
    m = res.max
    res.to_a.index(m)
  end

  def zero_vector(dim)
    Vector[*Array.new(dim) { 0 }]
  end

  def cost(parameters)
    sum = 0.0
    @xs.each_index do |i|
      res = log_hypothesis(parameters, @xs[i])
      sum += res[@ys[i]]
    end
    -1.0 * sum / @xs.size
  end

  def cost_gradient(parameters)
    sum = zero_vector(@xs[0].size / 4 + 1)
    #p (@xs[0].size / 4 + 1)
    @xs.each_index do |i|
      pirates = get_pirates(@xs[i])
      winner = @ys[i]
      #p (pirates[winner].size)
      sum += pirates[winner]
      probabilities = hypothesis(parameters, @xs[i])
      pirates.each_index do |k|
        #p probabilities
        #p pirates[k]
        sum -= probabilities[k] * pirates[k]
      end
    end
    -1.0 * sum / @xs.size
  end

  def gradient_descent(rate, monitor=nil, halt=nil)
    gd = GradientDescent.new(@parameters, rate, &method(:cost_gradient))
    gd.each_iter(&monitor).stop_when(&halt).run
    @parameters = gd.x
  end
end


def create_features(row)
  y = row[1] # winner!
  x = Vector[
    row[3], # s1
    row[4], # w1
    row[5], # o1
    row[6], # c1
    row[7], # f11
    row[8], # f12
    row[9], # f13
    row[10], # f14
    row[3] * row[3],
    row[3] * row[4],
    row[4] * row[4],
    row[3] * row[7],
    row[4] * row[7],
    row[3] * row[8],
    row[4] * row[8],
    row[3] * row[9],
    row[4] * row[9],
    row[3] * row[10],
    row[4] * row[10],
    row[7] * row[7],
    row[8] * row[8],
    row[9] * row[9],
    row[10] * row[10],
    row[12], # s2
    row[13], # w2
    row[14], # o2
    row[15], # c2
    row[16], # f21
    row[17], # f22
    row[18], # f23
    row[19], # f24
    row[12] * row[12],
    row[12] * row[13],
    row[13] * row[13],
    row[12] * row[16],
    row[13] * row[16],
    row[12] * row[17],
    row[13] * row[17],
    row[12] * row[18],
    row[13] * row[18],
    row[12] * row[19],
    row[13] * row[19],
    row[16] * row[16],
    row[17] * row[17],
    row[18] * row[18],
    row[19] * row[19],
    row[21], # s3
    row[22], # w3
    row[23], # o3
    row[24], # c3
    row[25], # f31
    row[26], # f32
    row[27], # f33
    row[28], # f34
    row[21] * row[21],
    row[21] * row[22],
    row[22] * row[22],
    row[21] * row[25],
    row[22] * row[25],
    row[21] * row[26],
    row[22] * row[26],
    row[21] * row[27],
    row[22] * row[27],
    row[21] * row[28],
    row[22] * row[28],
    row[25] * row[25],
    row[26] * row[26],
    row[27] * row[27],
    row[28] * row[28],
    row[30], # s4
    row[31], # w4
    row[32], # o4
    row[33], # c4
    row[34], # f41
    row[35], # f42
    row[36], # f43
    row[37], # f44
    row[30] * row[30],
    row[30] * row[31],
    row[31] * row[31],
    row[30] * row[34],
    row[31] * row[34],
    row[30] * row[35],
    row[31] * row[35],
    row[30] * row[36],
    row[31] * row[36],
    row[30] * row[37],
    row[31] * row[37],
    row[34] * row[34],
    row[35] * row[35],
    row[36] * row[36],
    row[37] * row[37]
  ]
  return x, y
end

def train_model(xs, ys)
  pp = Preprocessor.new(xs, ys)
  pp.standardize(regression=false)
  puts "preprocessing: #{pp.history}"
  sr = ModifiedSoftmax.new(pp.xs, pp.ys)
  monitor = lambda { |gd|
    print "\n[#{gd.iterations}: #{sr.cost(gd.x)}]"
    if gd.iterations % 25 == 0
      print "\n#{gd.x}\n"
    end
  }
  halt = lambda { |gd| gd.iterations > 1000 }
  sr.gradient_descent(2.0, monitor, halt)
  puts "\nparameters: #{sr.parameters}"
  return pp, sr
end


$stdout.sync = true
begin
  db = SQLite3::Database.open "data.db"
  data = load_data(db)
  train_xs = []
  train_ys = []
  xvalid_xs = []
  xvalid_ys = []
  test_xs = []
  test_ys = []
  count = 0
  # i have 7900 rows
  data.each do |row|
    x, y = create_features(row)
    if count >= 6000
      test_xs << x
      test_ys << y
    elsif count > 5000
      xvalid_xs << x
      xvalid_ys << y
    else
      train_xs << x
      train_ys << y
    end
    count += 1
  end

  # xvalidation
  pp = Preprocessor.new(train_xs, train_ys)
  pp.standardize(regression=false)
  processed_xs = xvalid_xs.map do |x|
    pp.pack(x)
  end
  sr = ModifiedSoftmax.new(processed_xs, xvalid_ys)
  sr.parameters = Vector[-0.07357259513452283, 0.0471735953694774, -0.3084823498288783, -0.20848966063582705, -0.24050208837493176, 0.5546748000059569, 0.1592115978830902, 0.3162208092145056, 0.6874588566464949, 2.1449386840474984, -0.7885298463042837, 0.9665661749992158, -0.06798077332664032, 0.08047653630736294, 0.14602948125054632, -0.3258734858643329, -1.1371897811553597, 0.34517703571537045, -0.23493813734226524, -0.6994483570335441, -0.05706281250598921, 0.03557878624561915, -0.024208263974604356, 0.06481856908830803]
  test1 = create_features([5180, 2,
    "", 74, 189, 11, 13, 2, 0, 1, 0,
    "", 79, 177, 6, 9, 1, 0, 1, 0,
    "", 81, 207, 2, 2, 4, 0, 1, 0,
    "", 76, 116, 5, 7, 1, 0, 2, 0])
  test2 = create_features([5180, 3,
    "", 81, 165, 2, 2, 2, 0, 2, 0,
    "", 52, 221, 11, 11, 4, 0, 3, 1,
    "", 73, 112, 5, 5, 2, 0, 4, 0,
    "", 68, 180, 2, 2, 3, 0, 2, 0])
  test3 = create_features([5180, 2,
    "", 61, 213, 13, 13, 0, 0, 2, 0,
    "", 59, 211, 5, 7, 2, 0, 0, 0,
    "", 76, 171, 4, 2, 4, 0, 3, 2,
    "", 79, 169, 2, 2, 1, 0, 3, 0])
  test4 = create_features([5180, 0,
    "", 93, 199, 2, 2, 3, 0, 1, 0,
    "", 82, 182, 6, 9, 1, 0, 0, 0,
    "", 66, 185, 13, 13, 1, 0, 1, 0,
    "", 81, 166, 5, 7, 1, 0, 1, 0])
  test5 = create_features([5180, 3,
    "", 89, 189, 4, 4, 1, 0, 2, 0,
    "", 71, 151, 5, 5, 5, 0, 0, 0,
    "", 87, 166, 2, 2, 1, 0, 1, 0,
    "", 73, 202, 9, 9, 1, 0, 1, 0])


  p sr.hypothesis(sr.parameters, pp.pack(test1[0]))
  p sr.hypothesis(sr.parameters, pp.pack(test2[0]))
  p sr.hypothesis(sr.parameters, pp.pack(test3[0]))
  p sr.hypothesis(sr.parameters, pp.pack(test4[0]))
  p sr.hypothesis(sr.parameters, pp.pack(test5[0]))
=begin
yay = 0
  total = 0
  sr.xs.each_index do |i|
    total += 1
    if sr.predict(processed_xs[i]) == xvalid_ys[i]
      yay += 1
    end
  end
  p yay, total
  #train_model(train_xs, train_ys)

  # naive "choose the best opening odds" test
  yay2 = 0
  xvalid_xs.each_index do |i|
    odds = [test_xs[i][2], test_xs[i][25], test_xs[i][48], test_xs[i][71]]
    p odds, odds.index(odds.min), xvalid_ys[i]
    if odds.index(odds.min) == xvalid_ys[i]
      yay2 += 1
    end
  end
  yay3 = 0
  # choose the best closing odds test
  xvalid_xs.each_index do |i|
    odds = [test_xs[i][3], test_xs[i][26], test_xs[i][49], test_xs[i][72]]
    if odds.index(odds.min) == xvalid_ys[i]
      yay3 += 1
    end
  end

  p yay2, total
  p yay3, total


  sr.parameters = parameters
  0.upto(100) do |i|
    #p xs[i]
    p sr.predict(pp.pack(xs[i]))
    if i % 5 == 4
      puts ""
    end
  end
=end
rescue SQLite3::Exception => e
  puts "Error: #{e}"
ensure
  db.close if db
end
