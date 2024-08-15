import os
from sqlalchemy import select
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.states as st
import app.keyboards as kb
import app.database.models as md
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Welcome! 👋\nHere you can create your own tasks and plans, follow and change them!", reply_markup=kb.main)
    await rq.set_user(message.from_user.username)


@router.message(Command(commands='menu') or F.text.lower() == 'menu')
async def cmd_menu(message: Message):
    await message.answer("From here you can come anywhere!", reply_markup=kb.main)


@router.callback_query(F.data == 'menu')
async def cmd_menu(callback: CallbackQuery):
    await callback.answer(None)
    await callback.message.answer("From here you can come anywhere!", reply_markup=kb.main)


@router.message(F.text == '📝 Your plans' or Command(commands='plans'))
async def all_plans(message: Message):
    all_plans = ""
    async with md.async_session() as session:
        list_query = select(md.ListOfTasks)
        task_query = select(md.Task)
        list_result = await session.execute(list_query)
        task_result = await session.execute(task_query)       
    for listOfTask in list_result.scalars().all():
        all_plans += f"{listOfTask.id}. {listOfTask.name}\nDescription: {listOfTask.description}\nImportance: {listOfTask.importance}\n"
        if (listOfTask.condition == 0):
            all_plans += "Condition: ❌Failed\n"
        elif (listOfTask.condition == 1):
            all_plans += "Condition: ✅Completed\n"
        elif (listOfTask.condition == 2):
            all_plans += "Condition: 🔄In progress\n"
        elif (listOfTask.condition == 3):
            all_plans += "Condiotion: 🕧Hasn't started\n"
        for task in task_result.scalars().all():
            if (task.parent_list == listOfTask.id):
                all_plans += f"[____{task.id}. {task.name}\n          Description: {task.description}\n          Importance: {task.importance}\n"
                if (listOfTask.condition == 0):
                    all_plans += "          Condition: ❌Failed\n\n"
                elif (listOfTask.condition == 1):
                    all_plans += "          Condition: ✅Completed\n\n"
                elif (listOfTask.condition == 2):
                    all_plans += "          Condition: 🔄In progress\n\n"
                elif (listOfTask.condition == 3):
                    all_plans += "          Condiotion: 🕧Hasn't started\n\n"
        all_plans += "\n"
    await message.answer(text=all_plans)


@router.message(Command(commands='new_list'))
async def cmd_new_list(message: Message):
    await message.answer("Creation of new list of tasks!\nAre you sure, that you want to do it?", reply_markup=kb.new_list_creation)


@router.callback_query(F.data == 'creare_new_list')
async def create_new_list(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.newList.name)
    await callback.answer(None)
    await callback.message.answer("Greate! Let's start with name! Because name is the face of list!", reply_markup=None)


@router.message(st.newList.name)
async def list_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(st.newList.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(st.newList.description)
    await message.answer("Very Nice!\nNow tell something about your list!\n\n\n" +
                         "Psss someone told me? that you can send '-' and you won't need to write a description😜")
    

@router.message(st.newList.description)
async def list_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(st.newList.importance)
    await message.answer("Wow! It's so interesting!\nBut we need to continue. \nWhat about importance? Choose between 0 and 10")


@router.message(st.newList.importance)
async def list_importance(message: Message, state: FSMContext):
    await state.update_data(importance=message.text)
    await state.set_state(st.newList.condition)
    await message.answer("Okay, now the last step! In what condition your list.\nSome examples for you:\n" +
                         "0 - Failed\n1 - Completed\n2 - In progrees\n3 - Hasn't statrted")


@router.message(st.newList.condition)
async def list_condition(message: Message, state: FSMContext):
    await state.update_data(condition=message.text)
    data = await state.get_data()
    obj = md.ListOfTasks(
        name = data['name'],
        user_id = int(data['user_id']),
        description = data['description'],
        importance = int(data['importance']),
        condition = int(data['condition'])
    )
    async with md.async_session() as session:
        session.add(obj)
        await session.commit()
    await state.clear()
    await message.answer("Your new cool list was added!😎")


@router.message(Command(commands='new_task'))
async def cmd_new_task(message: Message):
    await message.answer("Wow! You want to create a task? I hope, you have list for it!", reply_markup=kb.new_task_creation)


@router.callback_query(F.data == 'creare_new_task')
async def create_new_task(callback: CallbackQuery, state: FSMContext):
    await state.set_state(st.newTask.name)
    await callback.answer(None)
    await callback.message.answer("Well, let's start with super-mega-ultra-extra-cool name! I know you can do it!", reply_markup=None)


@router.message(st.newTask.name)
async def task_name(message: Message, state: FSMContext):
    all_lists = ""
    async with md.async_session() as session:
        query = select(md.ListOfTasks)
        result = await session.execute(query)       
    for listOfTask in result.scalars().all():
        all_lists += f"{listOfTask.id}. {listOfTask.name}\nDescription: {listOfTask.description}\n\n"
    await state.update_data(name=message.text)
    await state.set_state(st.newTask.user_id)
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(st.newTask.parent_list)
    await message.answer(text=f"Okay, now enter an id of list, that will connect to your task\n\n{all_lists}")


@router.message(st.newTask.parent_list)
async def task_parent_list(message: Message, state: FSMContext):
    await state.update_data(parent_list=message.text)
    await state.set_state(st.newTask.description)
    await message.answer("Greate! Now tell something about your task!")


@router.message(st.newTask.description)
async def task_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(st.newTask.importance)
    await message.answer(f"Do you know, what is next, {message.from_user.first_name}? Importance! Of corse from 0 to 10")


@router.message(st.newTask.importance)
async def task_importance(message: Message, state: FSMContext):
    await state.update_data(importance=message.text)
    await state.set_state(st.newTask.condition)
    await message.answer("And the last one is condition!\n0 - Failed\n1 - Completed\n2 - In progrees\n3 - Hasn't statrted")


@router.message(st.newTask.condition)
async def task_condition(message: Message, state: FSMContext):
    await state.update_data(condition=message.text)
    data = await state.get_data()
    obj = md.Task(
        name = data['name'],
        user_id = int(data['user_id']),
        parent_list = int(data['parent_list']),
        description = data['description'],
        importance = int(data['importance']),
        condition = int(data['condition'])
    )
    async with md.async_session() as session:
        session.add(obj)
        await session.commit()
    await state.clear()
    await message.answer("Okay, now your task was added!")


@router.message(Command(commands='help') or F.text.lower() == 'help' or F.text == '⚙ Help')
async def cmd_help(message: Message):
    await message.answer("If you can't do something, try 'menu'.\n" + 
                         "If you have another problems, text me @Rouruginn")

