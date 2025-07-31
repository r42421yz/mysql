import React, { useState, useEffect } from 'react';
import { Layout, Menu, Radio } from 'antd';
import ReactECharts from 'echarts-for-react';

const { Sider, Content } = Layout;

function Dashboard() {
  const [chartData, setChartData] = useState([]);
  const [selectedKey, setSelectedKey] = useState('country');
  const [chartType, setChartType] = useState('bar');

  useEffect(() => {
    fetch(`http://localhost:5000/api/chart?type=${selectedKey}`)
      .then(res => res.json())
      .then(data => 
        {
          console.log(`类型: ${selectedKey}`, data);
          setChartData(data);});
  }, [selectedKey]);

  const getBarOption = () => ({
    title: { text: `电影数据 - ${selectedKey}`},
    tooltip: {},
    xAxis: { data: chartData.map(item => item.name), axisLabel: { rotate: 30 } },
    yAxis: {},
    series: [{
      name: '数量',
      type: 'bar',
      data: chartData.map(item => item.value)
    }]
  });

  const getPieOption = () => ({
  title: { text: `电影数据 - ${selectedKey}`, left: 'center' },
  tooltip: { trigger: 'item' },
  legend: { orient: 'vertical', left: 'left' },
  series: [
    {
      name: '数量',
      type: 'pie',
      radius: '60%',
      data: chartData.map(item => ({
        name: item.name,
        value: item.value
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  });
  
  const getLineOption = () => ({
    title:{text: `电影数据趋势 - ${selectedKey}`},
    tooltip:{
        trigger: 'axis'
    },
    xAxis: {
        type :'category',
        data:chartData.map(item => item.name)
    },
    yAxis: {
        type:'value'
    },
    series: [{
        name:'数量',
        type:'line',
        data: chartData.map(item => item.value)
    }]
  });


  return (
    <Layout style={{ minHeight: '200vh' }}>
      <Sider>
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['country']}
          onClick={({ key }) => setSelectedKey(key)}
        >
          <Menu.Item key="country">按国家</Menu.Item>
          <Menu.Item key="genres">按类型</Menu.Item>
          <Menu.Item key="rating">按评分</Menu.Item>
          <Menu.Item key="year">按年份</Menu.Item>
          <Menu.Item key="director">按导演</Menu.Item>
          <Menu.Item key="actors">按演员</Menu.Item>


        </Menu>
      </Sider>
        <Layout>
        <Content style={{ padding: '20px' }}>
            {selectedKey !== 'year' && (
                <Radio.Group
                    value={chartType}
                    onChange={e => setChartType(e.target.value)}
                    style={{ marginBottom: 16 }}
                >
                    <Radio.Button value="bar">柱状图</Radio.Button>
                    <Radio.Button value="pie">饼图</Radio.Button>
                </Radio.Group>
            )}

            <ReactECharts
                key={selectedKey + chartType}
                option={
                    selectedKey === 'year'
                    ? getLineOption()
                    : chartType === 'bar'
                        ? getBarOption()
                        : getPieOption()
                }
                notMerge={true}
                lazyUpdate={true}
            />
        </Content>
        </Layout>

    </Layout>
  );
}

export default Dashboard;
