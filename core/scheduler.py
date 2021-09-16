'''
服务调度器：
1. 根据Icpc业务事件查找任务指令
2. 向Celery发送任务指令

'''

# 导入指令表
from .models import Instruction

# 导入任务
from .tasks import maintenance_operation_proc, operation_proc_create, operation_proc_update, operation_proc_delete, form_create, form_update

# 指令字典
tasks_dict = {
    'mop': maintenance_operation_proc,
}


# 1、查找指令
def find_instructions(event):
    instructions = Instruction.objects.filter()
    print(instructions)
    return instructions


# 2、发送任务指令
def send_instructions(instructions):
    for instruction in instructions:
        print(instruction)
        oid = instruction.oid
        ocode = instruction.ocode

        # 执行@task
        tasks_dict[instruction.oaction].delay(oid, ocode)
    return print('send_instructions')



# 调度器
def service_scheduler(event):
    instructions = find_instructions(event)
    send_instructions(instructions)
    return
