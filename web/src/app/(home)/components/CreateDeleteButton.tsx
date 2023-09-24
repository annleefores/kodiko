"use client";
import React from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

const CreateDeleteButton = () => {
  const router = useRouter();
  // TODO: Add auth
  const createPod = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_BACKEND}/create`
      );
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
    router.push("/code");
  };
  const deletePod = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_BACKEND}/delete`
      );
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="flex flex-col gap-y-6">
      <button
        onClick={createPod}
        className="transition ease-in-out delay-150 bg-blue-500  hover:bg-indigo-500 duration-300 p-1 px-10 border rounded-md border-blue-500"
      >
        Create
      </button>
      <button
        onClick={deletePod}
        className="transition ease-in-out delay-150 bg-red-500  hover:bg-red-600 duration-300 p-1 px-10 border rounded-md border-red-500"
      >
        Delete
      </button>
    </div>
  );
};

export default CreateDeleteButton;
