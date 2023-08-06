import pygrading.general_test as gg

def prework(job: gg.Job):
    # 自定义评测用例总分
    testcases = gg.create_testcase(100)

    for i in range(1, 5):
        input_src = i
        output_src = pow(2, i)

        # 使用append()方法向testcases追加评测用例
        testcases.append("TestCase{}".format(i), 25, input_src, output_src)

    job.set_testcases(testcases)


def run(job: gg.Job, testcase: gg.TestCases.SingleTestCase):
    print("######################")
    print("Name:", testcase.name)
    print("score:", testcase.score)
    print("input_src:", testcase.input_src)
    print("output_src:", testcase.output_src)
    print("extension:", testcase.extension)


myjob = gg.job(prework=prework, run=run, postwork=None)

myjob.start()